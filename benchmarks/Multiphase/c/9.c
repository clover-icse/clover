int main(){
    int x;

    // pre-conditions
    x = 0;

    // loop body
    while(unknown()){
        if(x == 9998){
            x = 1;
        }else{
            x = x + 2;
        }
    }

    // post-condition
    if(x %4 == 0){
        assert(x <= 9996);
    }
    
}